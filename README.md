<h1> Custom Newsletter </h1>

<h2> Introdução </h2>

<p>O objetivo desse projeto é criar um sistema composto por uma API de cadastro de usuarios e pedidos de produtos no qual serão registrado em uma base de dados, e a partir desses pedidos será realizado uma pesquisa automatica no site <a href="https://www.amazon.com.br/">Amazon</a> do produto cadastrado e periodicamente (semanalmente ou mensalmente) um email será enviado ao usuario informando o preço do(s) protudo(s) que ele escolheu</p>

<h2> Metodologias </h2>

<p>O projeto é dividido em 3 pilares, a API, o Crawler e o Sender, sendo todos controlados por um arquivo Main atraves de cron jobs ou agendador de tarefas. Todos os dados são armazenados em um banco de dados SQL, também são gerados logs para acompanhar o registro e fluxo das tarefas</p>

<h3>DataBase</h3>

<p>O banco de dados escolhido é um relacional(SQL) construido com a biblioteca <a href="https://docs.python.org/3/library/sqlite3.html">SQLite3</a>, e foi usado essa modelagem:</p>
<img src="/src/mer.png"height="500px" width="500px"/>

<h3>API</h3>

<p>A api foi construida utilizando a biblioteca <a href="https://flask.palletsprojects.com/en/2.2.x/">Flask</a>, é composta por 2 endpoints do tipo POST que recebem um Json, o primeiro endpoint é o de cadastro de usuario onde é recebido nome e email, apos a validação os dados, eles são salvos na base de dados em 'users'. O segundo endpoint é o de requisição onde é recebido um Json com o nome do produto (quanto mais especifico melhor sera o resultado da pesquisa), a frequencia que o usuario deseja receber emails, sendo 0 - nenhuma, 1 - semanal e 2 - mensal e também o email do usuario, apos as validações as requisições são salvas no banco</p>
<p>Nota: a api é executada separadamente do resto do projeto, para executar use o comando <code>python api.py</code></p>

<h3>Crawler</h3>

<p>O crawler sera responsavel por acessar o site da Amazon, fazer uma pesquisa e retornar o nome de mercado e preço do produto que o usuario selecionou e então salvar na base de dados, o crawler foi construido com <a href="https://selenium-python.readthedocs.io/">Selenium</a> e <a href="https://pypi.org/project/webdriver-manager/"></a>webdriver_manager e é executado semanalmente com os Cron Jobs</p>

<h3>Email Sender</h3>

<p>O Sender será executado semanalmente por cron jobs enviando informações se o ciclo é mensal ou semanal e então selecionara os usuarios desse ciclo consultando a base de dados, e com os dados do usuario sera feita outra consulta na base de dados para retornar o nome e preço dos produtos relacionados aquele usuario, um corpo de email sera criado e então enviado para o email que o usuario cadastrou no sistem, os emails são enviados usando as bibliotecas <a href="https://docs.python.org/3/library/smtplib.html">smtplib</a> e <a href="https://docs.python.org/3/library/ssl.html">ssl</a></p>
<p>Os dados da conta que enviara o email deve ser definido em um arquivo txt na raiz do projeto com o nome <code>senderemail.txt</code> com duas linhas sendo a primeira <code>email: xxxxx@gmail.com</code> e a segunda linha <code>password: *****</code></p>

<h3>Outros</h3>

<h4>Logger</h4>

<p>A biblioteca <a href="https://docs.python.org/3/library/logging.html">logging</a> foi configurada no arquivo log.py e é responsavel por registrar o fluxo de execução do programa no arquivo app.log que é gerado automaticamente</p>

<h4>Outras Libs</h4>

<p>Também são utilizadas outras bibliotecas auxiliares como: </p>
<ul>
<li><a href="https://pypi.org/project/email-validator/">email_validator</a> - para a validação de emails cadastrados por usuarios</li>
<li><a href="https://docs.python.org/3/library/datetime.html">datetime</a> - para melhorar a precisão das mensagens de log, inserindo o momento exato da execução dos processos</li>
<li><a href="https://docs.python.org/3/library/time.html">time</a> - para criar intervalos de execução dentro do Crawler e do Email Sender para evitar problemas de multiplas execuções</li>
<li><a href="https://docs.python.org/3/library/importlib.html">importlib</a> - com o reload para melhorar o uso do Logger</li>
</ul>

<h4>Como configurar Cron Jobs no windows: <a href="CRONJOBCONFIG.MD">Cron Job Config</a></h4>

<h3>Requisitos: </h3>
<ul>
<li><p><a href="https://www.python.org/">Python</a> - Para execução dos codigos</p></li>
<li><p><a href="https://www.google.com/intl/pt-BR/chrome/">Google Chrome</a> - Para execução do crawler</p></li>
<li><p><a href="https://www.google.com/intl/pt/gmail/about/">Gmail</a> - Para cadastrar uma conta como disparador de emails</p></li>
<li><p><a href="https://code.visualstudio.com/">Visual Studio Code</a> - Um editor de codigos</p></li>
<li><p><a href="https://git-scm.com/downloads">Git</a> - Para clonar e baixar esse repositorio</p></li>
<!-- <li><p><a href=""></a> - </p></li> -->
<li><p>Todas as bibliotecas citadas nesse documento</p></li>
</ul>

<h2>Conclusão</h2>

<h2>Proximos passos</h2>

<h4>API</h4>
<ul>
<li><p>Criar um endpoint DELETE para excluir usuarios</p></li>
<li><p>Criar um endpoint UPDATE para atualizar requisições</p></li>
<li><p>Criar um endpoint DELETE para excluir requisições</p></li>
<li><p>Criar um endpoint DELETE para excluir produtos</p></li>
<!-- <li><p></p></li> -->
</ul>

<h4>Crawler</h4>
<ul>
<li><p>Capturar os link dos produtos</p></li>
<li><p>Capturar imagens dos produtos</p></li>
</ul>

<h4>Sender</h4>
<ul>
<li><p>Incorporar link dos produtos ao email</p></li>
<li><p>Incorporar imagens dos produtos ao email</p></li>
</ul>

<!-- <h4>Main</h4>
<ul>
<li><p></p></li>
</ul> -->

<!-- <h4>DataBase</h4>
<ul>
<li><p></p></li>
</ul> -->
