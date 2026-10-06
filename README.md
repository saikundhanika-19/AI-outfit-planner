# StyleMind — Stage 3

Stage 3 adds the Digital Wardrobe.

## New functionality

- Upload clothing images.
- Save clothing images inside `uploads/`.
- Save wardrobe metadata in SQLite.
- View saved wardrobe items.
- Delete wardrobe items.
- Dashboard shows the number of wardrobe items.

## Important

Stage 3 uses **manual clothing details**.

AI image analysis is intentionally NOT implemented yet.

Stage 4 will connect a vision-capable AI model to analyze uploaded clothing images.

## Run

```powershell
streamlit run app.py
```

## Test

1. Make sure a user profile exists.
2. Open **👚 My Wardrobe**.
3. Upload a clothing image.
4. Enter an item name such as `White Shirt`.
5. Select the clothing details.
6. Click **Add to Wardrobe**.
7. The item should appear below the form.
8. Check that the dashboard wardrobe count increases.

## Folder created automatically

```text
StyleMind/
├── uploads/
└── data/
    └── stylemind.db
```
