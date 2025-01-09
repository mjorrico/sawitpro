# Deteksi Sawit Aerial View

## Usage
1. Konfigurasi environment

    ```bash
    pip install -r requirements.txt
    ```

2. Inference

    - Untuk palm detection problem

        ```bash
        python3 count.py --modelpath to/sawit/model.pt --imagepath to/your/image.jpg --target-tile-size 2048
        ```

        Flag `--modelpath` dan `--imagepath` wajib. Flag `--target-tile-size` opsional dijelaskan [disini](#tiling).

    - Untuk apple classification problem

        ```
        python3 (TODO)
        ```

    Output by default ada di `output.jpg`.

### Tiling

Dari [figure ini](figures/labels.jpg), rata-rata tinggi detector box sawit dari train set adalah ~9.5% tinggi input image (~7.5% untuk lebarnya). Model akan gagal untuk prediksi [gambar assignment ini](https://storage.googleapis.com/648010c1-f244-4641-98f2-73ff6c1b4e99/ai_assignment_20241202_count.jpeg) karena:

1. Ukuran sawit terlalu kecil (~4.5% input width). Kamera drone/satelit terlalu zoomed out.
2. Terlalu banyak sawit dalam satu frame.
    
Maka itu, gambar besar perlu di-_tiling_. Pakai flag `--target-tile-size` untuk set ukuran lebar _tile_-nya. Sederhananya, ukur lebar sebuah pohon sawit pakai [tool ini](https://www.rapidtables.com/web/tools/pixel-ruler.html) lalu bagi ~9.5%.

Kelemahannya adalah sawit ditepi tile kadang tidak terdeteksi.

## License and Usage Restrictions

This software is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license. See the [LICENSE](license/LICENSE-CC-BY-NC-ND-4.0.md) file for the full text.

### Purpose of This Software
This software is strictly created as part of a job application process for the position of **AI Engineer** at SawitPRO. It is intended solely for evaluation by the company as part of their hiring process.

### Restrictions
- **Non-Commercial Use**: This software may not be used for any commercial purposes.
- **No Derivatives**: The company may not modify, adapt, or create derivative works based on this software.
- **Attribution**: If the company shares or references this software, they must give appropriate credit to the author.

By accessing or using this software, the company agrees to these terms and conditions. Any use outside the scope of the job application process is strictly prohibited.