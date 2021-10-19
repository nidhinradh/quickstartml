mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = true\n\
[browser]\n\
serverAddress = \"quickstartml.herokuapp.com\"\n\
gatherUsageStats = true\n\
serverPort = $PORT\n\
\n\
" > ~/.streamlit/config.toml