use actix_files;
use actix_multipart::Multipart;
use actix_web::error::{self};
use actix_web::middleware::Logger;
use actix_web::web::Data;
use actix_web::{web, App, Error, HttpRequest, HttpResponse, HttpServer};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::{env, fs};

use futures::{StreamExt, TryStreamExt};

const MAX_SIZE: usize = 30 * 1024 * 1024;

async fn get_file(
    dir: web::Data<PathBuf>,
    id: web::Path<String>,
    req: HttpRequest,
) -> HttpResponse {
    let id = id.to_string();
    let filename = dir.join(id);

    if !Path::new(&filename).exists() {
        return HttpResponse::NotFound().body("File not found");
    }

    let file = actix_files::NamedFile::open_async(filename).await.unwrap();

    file.into_response(&req)
}

async fn put(
    dir: web::Data<PathBuf>,
    // mut payload: web::Payload,
    mut payload: Multipart,
) -> Result<HttpResponse, Error> {
    while let Some(mut field) = payload.try_next().await? {
        let content_disposition = field.content_disposition();

        if content_disposition.is_none() {
            continue;
        }

        let content_disposition = content_disposition.unwrap();
        let field_name = content_disposition.get_name().unwrap();

        if field_name != "file" {
            continue;
        }

        let filename = content_disposition.get_filename().unwrap_or("").to_string();
        let ext = filename.split(".").last().unwrap_or("bin");

        let id = uuid::Uuid::new_v4().to_string() + "." + ext;
        let filename = dir.join(&id);
        let mut file = fs::File::create(filename).unwrap();

        let mut total_size: usize = 0;

        while let Some(chunk) = field.next().await {
            let chunk = chunk?;

            total_size += chunk.len();

            if total_size > MAX_SIZE {
                return Err(error::ErrorPayloadTooLarge("File size exceeds 30MB limit"));
            }
            // body.extend_from_slice(&chunk);
            file.write(&chunk)?;
        }
        return Ok(HttpResponse::Ok().body(id));
    }

    Err(error::ErrorBadRequest("Missing file part"))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let dir = env::temp_dir().join("shibal_drive");
    fs::create_dir_all(&dir).unwrap();

    println!("{}", &dir.to_str().unwrap());

    HttpServer::new(move || {
        App::new()
            .wrap(Logger::new("%a %{User-Agent}i"))
            .app_data(Data::new(dir.clone()))
            .route("/get/{id}", web::get().to(get_file))
            .route("/put", web::post().to(put))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
