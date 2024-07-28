from celery import shared_task
from app.web.db.models import Pdf
from app.web.files import download
from app.chat import create_embeddings_for_md


@shared_task()
def process_document(md_id: int):
    md = Md.find_by(id=md_id)
    with download(md.id) as md_path:
        create_embeddings_for_md(md.id, md_path)
    
