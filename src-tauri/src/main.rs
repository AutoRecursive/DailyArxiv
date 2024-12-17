#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::{Command, Stdio};
use std::env;
use std::thread;
use std::io::{BufRead, BufReader};
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
            let current_dir = env::current_dir()
                .expect("Failed to get current dir");
            let project_root = current_dir.parent()
                .expect("Failed to get parent directory");
            
            #[cfg(target_os = "windows")]
            let python_cmd = "python";
            #[cfg(not(target_os = "windows"))]
            let python_cmd = "python3";

            // 使用 Stdio::piped() 来捕获输出
            let mut child = Command::new(python_cmd)
                .arg("-m")
                .arg("backend.main")
                .current_dir(&project_root)
                .env("PYTHONPATH", &project_root)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .expect("Failed to start backend");

            // 处理标准输出
            if let Some(stdout) = child.stdout.take() {
                thread::spawn(move || {
                    let reader = BufReader::new(stdout);
                    for line in reader.lines() {
                        if let Ok(line) = line {
                            println!("Backend stdout: {}", line);
                        }
                    }
                });
            }

            // 处理标准错误
            if let Some(stderr) = child.stderr.take() {
                thread::spawn(move || {
                    let reader = BufReader::new(stderr);
                    for line in reader.lines() {
                        if let Ok(line) = line {
                            eprintln!("Backend stderr: {}", line);
                        }
                    }
                });
            }

            // 在应用关闭时确保子进程也被终止
            let main_window = app.get_window("main").unwrap();
            main_window.on_window_event(move |event| {
                if let tauri::WindowEvent::CloseRequested { .. } = event {
                    if let Ok(mut child) = Command::new(python_cmd)
                        .arg("-c")
                        .arg("import psutil; [p.terminate() for p in psutil.Process().children()]")
                        .spawn() 
                    {
                        let _ = child.wait();
                    }
                }
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}