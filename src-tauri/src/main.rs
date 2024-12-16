#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use std::env;
use tauri::api::shell;
use tauri::Manager;

#[tauri::command]
async fn open_url(url: String, window: tauri::Window) {
    if let Err(e) = shell::open(&window.shell_scope(), url, None) {
        eprintln!("Failed to open URL: {}", e);
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![open_url])
        .setup(|app| {
            // 启动 Python 后端
            let current_dir = env::current_dir()
                .expect("Failed to get current dir");
            let project_root = current_dir.parent()
                .expect("Failed to get parent directory");
            let backend_path = project_root.join("backend");

            println!("Project root: {:?}", project_root);
            println!("Backend path: {:?}", backend_path);
            
            #[cfg(target_os = "windows")]
            let python_cmd = "python";
            #[cfg(not(target_os = "windows"))]
            let python_cmd = "python3";

            let result = Command::new(python_cmd)
                .arg("-m")
                .arg("backend.main")
                .current_dir(&project_root)  // 改为项目根目录
                .env("PYTHONPATH", &project_root)  // 设置 PYTHONPATH
                .spawn();

            match result {
                Ok(child) => {
                    println!("Backend started successfully with PID: {}", child.id());
                },
                Err(e) => {
                    println!("Failed to start backend: {}", e);
                    println!("Python command: {} -m backend.main", python_cmd);
                    println!("Working directory: {:?}", project_root);
                    panic!("Failed to start backend: {}", e);
                }
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}