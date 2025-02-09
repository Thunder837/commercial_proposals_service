import pandas as pd

def process_excel(input_filepath, output_filepath):
    # Загрузка Excel файла
    df = pd.read_excel(input_filepath)
    
    # Если столбец "Цена" существует, добавляем наценку (например, 20%)
    if 'Цена' in df.columns:
        df['Новая цена'] = df['Цена'] * 1.20
    
    # Удаляем столбец с контактной информацией, если он есть
    if 'Контакты' in df.columns:
        df = df.drop(columns=['Контакты'])
    
    # Сохранение обработанного файла
    df.to_excel(output_filepath, index=False)
