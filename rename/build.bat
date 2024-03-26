pyinstaller rename.spec --noconfirm
robocopy test dist/rename/raw /E
robocopy poppler dist/rename/poppler /E
cd dist/rename/
mkdir renamed
:: https://stackoverflow.com/a/42070127/4468834
