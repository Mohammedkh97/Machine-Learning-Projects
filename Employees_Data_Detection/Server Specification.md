
## 🖥️ For **Server (Production or Heavy OCR Inference)**

### ✅  Recommended Specs (Cloud/Bare Metal)

| Spec     | Value                             |
| -------- | --------------------------------- |
| GPU      | NVIDIA L40 / L4  (32GB) or         |
| CPU      | 8+ vCPUs                          |
| RAM      | 64 GB                             |
| SSD      | 100+ GB                           |
| Network  | 1 Gbps                            |
| Provider | Paperspace, AWS, Lambda, OVH          |
| Scale    | 1 server ≈ 15–20 documents/minute |
| OS      | Ubuntu 24.04 LTS Linux                                         |

### ✅ Recommended Bare-Metal Server Specs


| Component   | Recommended                                                             | Notes                                                          |
| ----------- | ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| **GPU**     | NVIDIA L40 / A40 / A10 / RTX 6000 ADA      | For Qwen2-VL inference (needs \~10–12GB VRAM)                  |
| **CPU**     | AMD EPYC 7003 series or Intel Xeon Gold (12+ cores)                     | Needed for multi-threaded preprocessing, parallel doc handling |
| **RAM**     | 64 GB DDR4 ECC                                                          | To buffer multiple document jobs            |
| **Disk**    | 128 GB NVMe SSD                                                           | Fast random read/write for PDF/image handling                  |
| **Network** | 1 Gbps or 10 Gbps uplink                                                | For Groq API latency-sensitive calls                           |
| **OS**      | Ubuntu 24.04 LTS Linux                                         | Good CUDA/PyTorch compatibility                                |
