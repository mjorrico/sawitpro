# SawitPRO Technical Round

By: Jordan Enrico

Aerial palm tree detection and apple classification all done using YOLO 11 pre-trained by Ultralytics. Palm tree detection requires finetuning. Apple classification doesn't require fine-tuning but involves segmentation followed by classical CV methods.


## Usage
1. Clone repository ([repo page](https://github.com/mjorrico/sawitpro)). Skip kalau sudah.

    ```bash
    $ git clone https://github.com/mjorrico/sawitpro.git
    ```
2. Konfigurasi environment

    ```bash
    $ pip install -r requirements.txt
    ```

3. Inference

    - Untuk palm detection problem

        ```bash
        $ python3 count.py --model models/count.pt --image to/your/image.jpg --target-tile-size 2048 --output sawit-detected.jpg
        ```

        Options `--model` dan `--image` wajib. Option `--target-tile-size` opsional dijelaskan [disini](#tiling). Useful untuk image yang sawitnya banyak dan/atau kecil. Option `--output` juga opsional. By default, disimpan di `output.jpg`. Untuk show help, jalankan:

        ```bash
        $ python3 count.py --help
        ```

    - Untuk apple classification problem

        ```bash
        $ python3 classify.py --image to/your/image.jpg --output your/output/directory --seg
        ```

        Option `--image` wajib. Options `--output` dan flag `--seg` opsional. Option `--output` untuk specify **directory** output yang defaultnya di _current directory_. Flag `--seg` untuk output segmentation applenya. Untuk help, jalankan:

        ```bash
        $ python3 classify.py --help
        ```

### Tiling

Dari [figure ini](figures/labels.jpg), rata-rata tinggi detector box sawit dari train set adalah ~9.5% tinggi input image (~7.5% untuk lebarnya). Model akan gagal untuk prediksi [gambar assignment ini](https://storage.googleapis.com/648010c1-f244-4641-98f2-73ff6c1b4e99/ai_assignment_20241202_count.jpeg) karena:

1. Ukuran sawit terlalu kecil (~4.5% input width). Kamera drone/satelit terlalu zoomed out. YOLO lemah deteksi objek kecil. Saat resize ke `640px`, information loss.
2. Terlalu banyak sawit dalam satu frame.
    
Maka itu, gambar besar perlu di-_tiling_. Pakai option `--target-tile-size` untuk set ukuran lebar _tile_-nya. Sederhananya, ukur lebar sebuah pohon sawit pakai [tool ini](https://www.rapidtables.com/web/tools/pixel-ruler.html) lalu bagi ~9.5%.

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