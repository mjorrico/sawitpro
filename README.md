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

    **Note:** environment takes 6GB of space and network.

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

This software is licensed under the **GNU Affero General Public License version 3 (AGPL-3.0)**. See the [LICENSE](LICENSE.md) file for the full text.

### Purpose of This Software
This software was originally created as part of a job application process for the position of **AI Engineer** at SawitPRO. While it was initially intended for evaluation by the company as part of their hiring process, it is now available under the AGPL license, which grants additional freedoms and responsibilities to users.

### Key Features of the AGPL License
- **Freedom to Use**: This software can be used for any purpose, including commercial use.
- **Freedom to Modify**: Users are allowed to modify, adapt, and create derivative works based on this software.
- **Freedom to Share**: Users can distribute the original or modified versions of this software.
- **Copyleft Requirement**: If you distribute modified versions of this software or use it to provide a service over a network (e.g., as a web application), you must also license your modifications under the AGPL and make the source code available to users. This ensures that the software and its derivatives remain free and open-source.

### Attribution
If you share or modify this software, you must provide appropriate credit to the original author and include a copy of the AGPL license. You must also indicate if changes were made.

By accessing, using, or modifying this software, you agree to comply with the terms and conditions of the AGPL license. This license ensures that the software remains free and open-source, fostering collaboration and innovation while protecting the rights of the original author and the community.