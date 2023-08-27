from fastapi import APIRouter
import re
from PIL import Image
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile, HTTPException
from scanner.modules.tasks.task import *
router = APIRouter()


sys.path.insert(0, str(config.ROOT_DIR))


@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        ocr_result = perform_ocr(image)

        if ocr_result:
            content = ocr_result.strip()

            if is_meaningful_content(content):
                findings = []

                credit_card_pattern = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
                email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
                url_pattern = re.compile(r"\b(?:https?://|www\.)\S+\b")
                ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
                domain_pattern = re.compile(r"\b(?:[A-Za-z0-9.-]+)\.[A-Z|a-z]{2,}\b")
                date_pattern = re.compile(r"\b(?:\d{2}[-/.]\d{2}[-/.]\d{4})\b")
                combolist_pattern = re.compile(
                    r"\b(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}):[A-Za-z0-9.-]+\b")
                id_number_pattern = re.compile(r"\b(?:\d{11})\b")
                plate_pattern = re.compile(r"\b[A-Z0-9]{2,10}\b")

                credit_cards = credit_card_pattern.findall(content)
                emails = email_pattern.findall(content)
                urls = url_pattern.findall(content)
                ips = ip_pattern.findall(content)
                domains = domain_pattern.findall(content)
                dates = date_pattern.findall(content)
                combolists = combolist_pattern.findall(content)
                id_numbers = id_number_pattern.findall(content)
                plates = plate_pattern.findall(content)

                for card in credit_cards:
                    card_value = card.replace(" ", "")
                    if validate_credit_card(card_value):
                        findings.append({"value": card, "type": "CREDIT_CARD"})
                    else:
                        findings.append({"value": card, "type": "INVALID_CREDIT_CARD"})
                for email in emails:
                    findings.append({"value": email, "type": "EMAIL"})
                for url in urls:
                    findings.append({"value": url, "type": "URL"})
                for ip in ips:
                    findings.append({"value": ip, "type": "IP"})
                for domain in domains:
                    findings.append({"value": domain, "type": "DOMAIN"})
                for date in dates:
                    findings.append({"value": date, "type": "DATE"})
                for combolist in combolists:
                    findings.append({"value": combolist, "type": "COMBOLIST"})
                for id_number in id_numbers:
                    findings.append({"value": id_number, "type": "ID_NUMBER"})
                for plate in plates:
                    if validate_address(plate):
                        findings.append({"value": plate, "type": "PLATE"})
                    else:
                        findings.append({"value": plate, "type": "INVALID_PLATE"})

                response_content = {"status": "successful", "content": content, "findings": findings}
                return JSONResponse(content=response_content, status_code=200)
            else:
                return JSONResponse(content={"status": "bad request. wrong file format."}, status_code=400)
        else:
            raise HTTPException(status_code=400, detail="bad request. wrong file format.")

    except Exception as e:
        raise HTTPException(status_code=204, detail=str(e))
