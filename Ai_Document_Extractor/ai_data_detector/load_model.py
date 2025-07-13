# file: load_model.py
from transformers import AutoProcessor, AutoModelForImageTextToText
import torch
import time
from read_pdf import download_and_convert_pdf_to_image


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the size dictionary with the required keys
# These values are based on the error message's suggested default if size is None
# You might need to adjust these based on the specific model documentation if available
processor_kwargs = {"size": {"shortest_edge": 56 * 56, "longest_edge": 28 * 28 * 1280}}

# Load model from local path

model_path = r"/home/developer/Dev/Qwen2-VL-2B-OCR"

processor = AutoProcessor.from_pretrained(model_path, **processor_kwargs)

model = AutoModelForImageTextToText.from_pretrained(
    model_path, torch_dtype=torch.float16
)  # Move model to the specified device (GPU or CPU)

# Move model to the right device
model = model.to(device)
conversation = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
            },
            {
                "type": "text",
                "text": (
                    "Extract all the data from the image, headlines and don't miss any"
                ),
            },
        ],
    }
]

def inference(url, employee_id):
    print("[INFO] Starting inference...\n")

    # Clear GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    # Step 1: Download PDF and convert first page to image
    img = download_and_convert_pdf_to_image(url, f"files/{employee_id}.pdf")
    if img is None:
        print("[ERROR] Failed to convert PDF to image.")
        return None

    # Step 2: Build dynamic conversation

    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                },
                {
                    "type": "text",
                    "text": (
                        "Extract all the data from the image, headlines and don't miss any"
                    ),
                },
            ],
        }
    ]

    # Preprocess the inputs
    # Preprocess the inputs
    text_prompt = processor.apply_chat_template(
        conversation, add_generation_prompt=True
    )
    # Excepted output: '<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n<|vision_start|><|image_pad|><|vision_end|>Describe this image.<|im_end|>\n<|im_start|>assistant\n'

    inputs = processor(
        text=[text_prompt], images=[img], padding=True, return_tensors="pt"
    )
    inputs = inputs.to("cuda")
    # Move input tensors to the same device
    # inputs = {
    #     k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()
    # }

    start = time.time()
    # Inference: Generation of the output
    output_ids = model.generate(**inputs, max_new_tokens=2048)
    # generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(inputs.input_ids, output_ids)
    ]

    output_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
    )

    elapsed = time.time() - start
    print("[INFO] Inference completed.")
    print("|========================================|")
    print(f"|         Inference time: {elapsed:.2f} sec       |")
    print("|========================================|")


    return output_text[0]


if __name__ == "__main__":
    url = "https://americanamc-ammc-develop-21331446.dev.odoo.com/web/content/13542"
    # url = "http://149.102.141.44:8066/web/content/80106"
    employee_id = "12345"
    # print(inference(url, employee_id))
    text = inference(url, employee_id)
    print(text)
