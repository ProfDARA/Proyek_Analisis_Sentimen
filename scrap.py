import pandas as pd
from google_play_scraper import reviews
import re


# Scraping Ulasan Aplikasi dari Google Play Store
def scrape_reviews(app_id: str, count: int = 150000, lang: str = 'id') -> pd.DataFrame: #count int diisi sebanyak 60000 data misalnya
    result, _ = reviews(app_id, lang=lang, count=count)
    df = pd.DataFrame(result)
    # bagian berisi kolom yang ingin kita ambil
    df = df[['userName', 'content', 'score', 'at']]
    return df

# bagian ini untuk memberi label pada skor
def label_sentiment(score: int) -> str:
    if score <= 2:
        return "negatif"
    elif score == 3:
        return "netral"
    else:
        return "positif"

# Fungsi untuk membersihkan komentar kosong dan menghapus emoji
def clean_comment(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # Hapus emoji dan karakter non-teks
    text = re.sub(r'[^\w\s,.!?@#:/\-]', '', text, flags=re.UNICODE)
    # Hapus spasi di awal/akhir
    text = text.strip()
    return text

# Fungsi untuk menyiapkan dataset dengan jumlah seimbang untuk setiap label
def prepare_dataset(app_id: str, output_path: str = "dataset_labeled.csv") -> pd.DataFrame:
    df = scrape_reviews(app_id)
    df.drop_duplicates(subset=["content"], inplace=True)
    df.dropna(subset=["content"], inplace=True)
    # Bersihkan komentar
    df["content"] = df["content"].apply(clean_comment)
    # Hapus baris dengan komentar kosong setelah dibersihkan
    df = df[df["content"].str.strip() != ""]
    df["label"] = df["score"].apply(label_sentiment)

    # percobaan mengambil masing-masing 50000 data untuk setiap label
    df_positif = df[df["label"] == "positif"].sample(n=50000, random_state=42) if len(df[df["label"] == "positif"]) >= 50000 else df[df["label"] == "positif"]
    df_negatif = df[df["label"] == "negatif"].sample(n=50000, random_state=42) if len(df[df["label"] == "negatif"]) >= 50000 else df[df["label"] == "negatif"]
    df_netral = df[df["label"] == "netral"].sample(n=50000, random_state=42) if len(df[df["label"] == "netral"]) >= 50000 else df[df["label"] == "netral"]

    df_balanced = pd.concat([df_positif, df_negatif, df_netral])
    df_balanced = df_balanced[["userName", "content", "score", "label", "at"]]
    df_balanced.to_csv(output_path, index=False)

    print(f"Dataset berhasil disimpan: {output_path}")
    return df_balanced

# Contoh penggunaan, saya mereview aplikasi Mobile BPJS misalnya
if __name__ == "__main__":
    app_id = 'app.bpjs.mobile'
    prepare_dataset(app_id)