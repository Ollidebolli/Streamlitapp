mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"oliver.de.boer.moran@sap.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
