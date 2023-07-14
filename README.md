# Simulador_CircuitosEletricosSenoidais_PythonTkinter
Este é um simulador de circuitos elétricos senoidais desenvolvido em Python, utilizando a biblioteca Tkinter para a criação da interface gráfica. O objetivo do projeto é permitir a análise e obtenção das tensões nos nós e correntes nos ramos de circuitos elétricos senoidais de forma interativa e intuitiva. A lógica utilizada é baseada em uma análise nodal, o que permite calcular a maioria dos circuitos. Embora o projeto esteja funcional, alguns circuitos particulares podem exigir a implementação de lógicas adicionais, como super nós. Portanto, sinta-se à vontade para adicionar novas funcionalidades ao simulador.


## Exemplo de configuração do circuito

A configuração do circuito deve ser feita no painel do Tkinter que irá abrir ao executar o arquivo main.py

O arquivo "saida.txt" é desta forma:

```text
1   2   10   None   None   20   None
2   3   5    None   None   None   2
3   1   None   0.01   None   None   None
```

Cada linha representa uma conexão entre dois nós do circuito. Os campos separados por tabulação são, respectivamente, o nó de origem, o nó de destino, a resistência (em ohms), a indutância (em henries), a capacitância (em farads), a tensão (em volts) e a corrente (em amperes).



## Funcionalidades

Este simulador de circuitos elétricos senoidais possui as seguintes funcionalidades principais:

1. **Entrada de Dados**: Os usuários podem adicionar linhas ao circuito especificando os componentes, como resistores, indutores, capacitores, fontes de tensão e corrente, através de campos de entrada fornecidos pela interface gráfica.

2. **Cálculo e Visualização**: O simulador realiza cálculos com base nas informações inseridas pelos usuários e exibe os resultados das tensões nos nós do circuito e correntes em cada componente. As informações são exibidas em caixas de texto na interface gráfica.

3. **Alternância de Domínio**: Os usuários podem alternar entre os domínios do tempo e da frequência para realizar a análise do circuito. A escolha do domínio é feita através de caixas de seleção na interface.

4. **Alteração de Circuitos**: O simulador permite que os usuários alterem os valores dos componentes existentes no circuito. Uma funcionalidade dedicada permite a atualização de valores específicos de cada componente.

## Uso do Simulador

Para utilizar o simulador de circuitos elétricos senoidais com Tkinter, siga as etapas abaixo:

1. **Adicionar Componentes**: Preencha os campos de entrada na interface gráfica com as informações dos componentes de circuito desejados, como nó de origem, nó de saída, resistência, indutância, capacitância, fonte de tensão e fonte de corrente.

2. **Alternar Domínio**: Selecione o domínio do tempo ou da frequência através das caixas de seleção correspondentes. Isso definirá o tipo de análise a ser realizada.

3. **Calcular**: Clique no botão "Calcular" para que o simulador processe os dados inseridos e exiba os resultados das tensões nos nós e correntes em cada componente.

4. **Visualizar Resultados**: Os resultados das tensões nos nós e correntes serão exibidos nas caixas de texto da interface gráfica. Os valores serão atualizados de acordo com as configurações do circuito.

5. **Alterar Circuitos**: Caso deseje alterar os valores dos componentes existentes, clique no botão "Alterar linhas". Uma nova janela será aberta, permitindo a modificação dos valores individuais dos componentes do circuito.

## Requisitos de Sistema

Para executar o simulador de circuitos elétricos senoidais com Tkinter, você precisa ter o Python instalado no seu sistema. O código foi testado na versão 3.11 do Python, mas pode ser compatível com versões anteriores.

Além disso, é necessário ter as seguintes bibliotecas instaladas (Estás bibliotecas são as mais importantes, embora algumas provavelmente já entejam  instaladas em sua máquina):

- Tkinter: Pode ser instalada com o comando `pip install tk` ou `pip install python-tk`. 
- PyPDF2: Pode ser instalada com o comando `pip install PyPDF2`.
- Sympy: Biblioteca para matemática simbólica em Python. Pode ser instalada com o comando `pip install sympy`.

Certifique-se de instalar as bibliotecas acima usando o gerenciador de pacotes `pip` antes de executar o simulador.

## Nota

Este projeto foi feito como parte da disciplina Eletricidade Para Computação II, no curso de Engenharia Da Computação na Universidade Federal da Paraíba.

