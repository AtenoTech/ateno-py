from .utils import to_base64

class RoomsService:
    def __init__(self, client):
        self.client = client

    def generate_room_2d(self, payload, on_progress=None):
        if on_progress:
            on_progress('Converting image and preparing request…')

        base64_image = to_base64(payload.get("image"))

        formatted_payload = {
            "aspectRatio": "16:9",
            "resolution": "2K"
        }
        formatted_payload.update(payload)
        formatted_payload["image"] = base64_image

        if on_progress:
            on_progress('Generating room design…')

        result = self.client.post('/rooms/analyze-and-generate', formatted_payload)

        summary = result.get("summary") or {}
        workflow = result.get("workflow") or {}
        generate = workflow.get("generate") or {}

        design_id = result.get("designId") or summary.get("designId") or workflow.get("designId")
        design_save_error = result.get("designSaveError") or summary.get("designSaveError")
        
        generated_image = (
            generate.get("image") or 
            generate.get("roomImage_result") or 
            result.get("image") or 
            result.get("generatedImage") or 
            summary.get("image")
        )

        return {
            "raw": result,
            "generatedImage": generated_image,
            "designId": design_id,
            "designSaveError": design_save_error
        }

    def generate_room_3d(self, payload, on_progress=None):
        if not payload.get("imageBase64") and not payload.get("roomImage"):
            raise ValueError("[AtenoSDK] At least one of imageBase64 or roomImage is required")

        if on_progress:
            on_progress('Processing images…')

        image_payload = {}
        if payload.get("imageBase64"):
            image_payload["imageBase64"] = to_base64(payload.get("imageBase64"))
        if payload.get("roomImage"):
            image_payload["roomImage"] = to_base64(payload.get("roomImage"))

        formatted_payload = {**payload, **image_payload}

        if on_progress:
            on_progress('Generating 3D space…')

        result = self.client.post('/rooms/generate-space', formatted_payload)

        summary = result.get("summary") or {}
        workflow = result.get("workflow") or {}

        storage_url = result.get("storageUrl") or summary.get("storageUrl") or workflow.get("storageUrl")
        design_id = result.get("designId") or summary.get("designId")
        
        firebase_saved_val = result.get("firebaseSaved")
        firebase_saved = firebase_saved_val is True or str(firebase_saved_val).lower() == 'true'
        firebase_path = result.get("firebasePath") or result.get("firebase_gs_path")

        return {
            "raw": result,
            "storageUrl": storage_url,
            "designId": design_id,
            "firebaseSaved": firebase_saved,
            "firebasePath": firebase_path
        }