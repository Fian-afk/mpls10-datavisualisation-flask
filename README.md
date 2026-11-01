# Dashboard MPL Indonesia Season 10 (Flask + Chart.js)

Dashboard ini memvisualisasikan statistik hero MPL ID Season 10 dari
`data/MPL_ID_S10.csv`, termasuk jumlah pick, ban, dan win rate.

## Menjalankan

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000 di browser. Chart.js dimuat dari CDN, jadi perlu koneksi internet.

## Endpoint API

| URL | Isi |
|---|---|
| `/` | Halaman dashboard |
| `/api/ringkasan` | Jumlah hero, total pick dan ban, win rate keseluruhan, serta hero dengan total pick + ban tertinggi |
| `/api/statistik-hero` | 10 hero paling sering di-pick, paling sering di-ban, dan dengan win rate tertinggi |

Peringkat win rate hanya menyertakan hero yang memiliki minimal 10 kali pick
agar perbandingan tidak didominasi hero dengan sampel pertandingan yang sangat kecil.
