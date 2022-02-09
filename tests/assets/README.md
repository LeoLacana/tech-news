Esta é a pasta de assets a serem utilizados durante os testes.

Arquivos .pickle:
    - São respostas http da biblioteca requests, serializadas com a biblioteca Pickle para que possamos fazer os testes sem realizar requisições reais.

Arquivo cached_news.json:
    - Contém o resultado final do scrape de várias notícias, para testarmos o funcionamento do scraper.

Arquivo test_assets.py:
    - É onde carregamos o cached_news.json, e onde temos também os links das notícias encontradas na pagina Novidades, usados para testar o scrape.

Pasta tecmundo_pages:
    - Esta pasta contem páginas html obtidas do site tecmundo, para fazermos os nossos testes sem precisar mandar requisições reais para o site. O nome de arquivo utilizado é obtido através da URI da página, retirando o domínio, substituindo os "/" por "|" e adicionando ".html" no final.
    Exceto "novidades.html" e novidades page 2.
    
