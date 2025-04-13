use std::env; // <-- Add this import
use std::fs::{self, File};
use std::io::{self, Read}; // <-- Added Write for io::copy
use std::path::{Path, PathBuf};
use zip::{write::FileOptions, ZipWriter, CompressionMethod};
use regex::Regex;

fn main() -> io::Result<()> {

    // 1. Get the current working directory (where the executable is run, typically the project root)
    let current_dir = env::current_dir()?;
    println!("Current directory: {:?}", current_dir); // Optional: for debugging

    // 2. Get the parent directory
    let parent_dir = current_dir.parent()
        .ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not determine parent directory"))?;
    println!("Parent directory: {:?}", parent_dir); // Optional: for debugging

    // 3. Construct the path to the target folder (assuming its name is "AB_Flow")
    //    Change "AB_Flow" if the target folder in the parent directory has a different name.
    let folder_to_zip = parent_dir.join("crystal_generator");
    println!("Target folder to zip: {:?}", folder_to_zip); // Optional: for debugging

    // Check if the target directory exists before proceeding
    if !folder_to_zip.is_dir() {
        return Err(io::Error::new(io::ErrorKind::NotFound,
            format!("Target directory not found at expected location: {:?}", folder_to_zip)
        ));
    }

    // Extract version from __init__.py inside the target folder
    let init_path = folder_to_zip.join("__init__.py");
    let version = extract_version(&init_path)?;

    // Construct the output zip file name based on the folder name and version
    // The zip file will be created in the *parent* directory alongside the target folder.
    // If you want the zip file created elsewhere (e.g., in the rust project dir),
    // adjust the path here. For example: `let zip_file_name = current_dir.join(format!("AB-Flow_{}.zip", version));`
    let zip_file_name = parent_dir.join(format!("crystal_generator_{}.zip", version));
    // let zip_file_name = folder_to_zip.with_file_name(format!("AB-Flow_{}.zip", version)); // Original way, creates zip next to the source folder


    // Open the zip file for writing
    let zip_file = File::create(&zip_file_name)?;
    let mut zip = ZipWriter::new(zip_file);

    // Options for compression
    let options = FileOptions::default()
        .compression_method(CompressionMethod::Deflated)
        .unix_permissions(0o755);

    // Recursively add files to the zip archive
    let folder_name = folder_to_zip
        .file_name()
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Could not get folder name"))?
        .to_string_lossy()
        .to_string(); // Convert to owned String
    zip_dir(&folder_to_zip, &folder_to_zip, &mut zip, &folder_name, options)?;

    // Finish the zip archive
    zip.finish()?;

    println!(
        "Folder {:?} has been zipped into {:?}",
        folder_to_zip, zip_file_name
    );

    Ok(())
}

fn extract_version(init_file_path: &PathBuf) -> io::Result<String> {
    let mut file = File::open(init_file_path).map_err(|e| {
        io::Error::new(e.kind(), format!("Failed to open {:?}: {}", init_file_path, e))
    })?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;

    // Adjusted regex to be more robust against whitespace variations
    let re = Regex::new(r#"(?m)^\s*['"]?version['"]?\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"#)
                .expect("Invalid Regex pattern"); // Use expect for unrecoverable regex errors

    if let Some(caps) = re.captures(&content) {
         // Use captures by index (0 is the full match, 1, 2, 3 are the groups)
        return Ok(format!("{}_{}_{}", &caps[1], &caps[2], &caps[3]));
    }

    Err(io::Error::new(io::ErrorKind::NotFound, format!("Version pattern not found in {:?}", init_file_path)))
}

fn zip_dir(
    base_dir: &Path,
    current_dir: &Path,
    zip: &mut ZipWriter<File>,
    base_name: &str,
    options: FileOptions<()>,
) -> io::Result<()> {
    for entry in fs::read_dir(current_dir)? {
        let entry = entry?;
        let path = entry.path();
        let entry_name = path.file_name().and_then(|name| name.to_str());

        const DIRS_TO_SKIP: [&str; 3] = ["tests", "__pycache__", "docs"];
        // Skip specific directories and hidden files/dirs (starting with .)
        if entry_name.map_or(false, |name| name.starts_with('.')) ||
           (path.is_dir() && entry_name.map_or(false, |name| DIRS_TO_SKIP.contains(&name))) {
            // println!("Skipping: {:?}", path); // Optional: for debugging
            continue;
        }

        // Calculate the path relative to the base directory being zipped
        let relative_path = path.strip_prefix(base_dir)
            .map_err(|e| io::Error::new(io::ErrorKind::Other,
                format!("Failed to strip prefix {:?} from {:?}: {}", base_dir, path, e)
            ))?;

        // Construct the name for the entry within the zip file
        // Use path::MAIN_SEPARATOR for platform-correct paths inside the zip if needed,
        // but zip standard typically uses '/'
        let name_in_zip = PathBuf::from(base_name).join(relative_path)
                                   .to_string_lossy()
                                   .replace('\\', "/"); // Ensure forward slashes in zip


        if path.is_dir() {
            // Add the directory entry (important for empty dirs)
            // Ensure the name ends with a slash for directories
            zip.add_directory(format!("{}/", name_in_zip), options)?;
            // Recurse into the directory
            zip_dir(base_dir, &path, zip, base_name, options)?;
        } else {
            // Add the file to the zip file
            // println!("Adding file: {:?} as {}", path, name_in_zip); // Optional: for debugging
            zip.start_file(name_in_zip, options)?;
            let mut file = File::open(&path)?;
            io::copy(&mut file, zip)?;
        }
    }
    Ok(())
}