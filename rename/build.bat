pyinstaller rename.spec --noconfirm
cd dist/rename/
robocopy test dist/rename/raw /E
mkdir renamed
robocopy poppler dist/rename/poppler /E
:: https://stackoverflow.com/a/42070127/4468834
