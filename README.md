# 🚗 Automação de Extração de Dados do Uber Driver

Este script automatiza a extração de dados de corridas da plataforma Uber Driver, coletando informações detalhadas sobre ganhos, corridas e atividades.

## 📋 Funcionalidades

- **Autenticação Automática**: Reutiliza cookies salvos para evitar login manual repetitivo
- **Extração de Dados**: Coleta informações completas de cada corrida
- **Múltiplos Dias**: Processa dados de diferentes dias automaticamente
- **Persistência**: Salva dados em formato *JSON* para análise posterior

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Selenium WebDriver** - Automação do navegador
- **undetected-chromedriver** - ChromeDriver não detectável
- **JSON** - Armazenamento de dados

## Primeira Execução

Na primeira execução, o script irá:
1. Abrir o navegador Chrome
2. Navegar para a página de login do Uber Driver
3. Aguardar **2 minutos** para login manual
4. Salvar os cookies de autenticação
5. Iniciar a extração automática

### 4. Execuções Subsequentes

Nas próximas execuções, o script:
- Reutiliza os cookies salvos
- Pula o processo de login manual
- Inicia diretamente a extração

## 📊 Dados Extraídos

Para cada corrida, o script coleta:

| Campo | Descrição |
|-------|-----------|
| **Ganhos** | Valor total ganho na corrida |
| **Tipo de Corrida** | Categoria da corrida |
| **Data** | Data da corrida |
| **Hora** | Horário da corrida |
| **URL do Mapa** | Link para visualização do trajeto |
| **Duração** | Tempo total da corrida |
| **Distância** | Quilometragem percorrida |
| **Endereço Coleta** | Local de origem |
| **Endereço Destino** | Local de destino |
| **Pontos Ganhos** | Pontos de fidelidade Uber Pro |
| **Valor Total Passageiro** | Valor pago pelo passageiro |
| **Descontos** | Descontos aplicados por promoções para usuários|
| **Meus Ganhos** | Valor líquido recebido |
| **Ganhos Uber** | Comissão da Uber |

## ⚙️ Configuração

### Dias de Extração

Por padrão, o script extrai dados semanais, selecionando um dia por vez: **8, 12, 18, 25**

```python
dias_para_puxar = ['8', '12', '18', '25']
```

### Timeouts

- **Login manual**: 120 segundos
- **Carregamento de página**: 20-30 segundos
- **Aguardo entre ações**: 2-5 segundos

## 📁 Estrutura de Arquivos

```
Uber_Driver/
├── uber_copy.py              # Script principal
├── uber_activities.json      # Dados extraídos
├── uber_cookies.json         # Cookies de autenticação
├── chromedriver.exe          # Driver do Chrome
├── chrome_profile_uber/      # Perfil do navegador
└── README.md                 # Este arquivo
```

## 📈 Análise dos Dados

Os dados são salvos em `uber_activities.json` no formato:

```json
[
  {
    "Ganhos": 15.50,
    "Tipo de Corrida": "UberX",
    "Data": "15/12/2024",
    "Hora": "14:30",
    "URL do Mapa": "https://...",
    "Duracao": "25 min",
    "Distancia": "8.5 km",
    "Endereco_Coleta": "Rua A, 123",
    "Endereco_Destino": "Rua B, 456",
    "Pontos_Ganhos": "Pontos ganhos: 2",
    "Valor_Total_Passageiro": "R$ 18,00",
    "Descontos": "R$ 2,50",
    "Meus_Ganhos": "R$ 15,50",
    "Ganhos_Uber": "R$ 2,50"
  }
]
```

## ⚠️ Avisos Importantes

- **Uso Responsável**: Este script é para fins educacionais e de análise pessoal
- **Termos de Uso**: Respeite os termos de serviço do Uber
- **Dados Pessoais**: Mantenha os dados extraídos em segurança
- **Atualizações**: A interface do Uber pode mudar, exigindo atualizações no script

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto é para uso educacional e pessoal. Use com responsabilidade.

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique a seção de solução de problemas
- Abra uma issue no repositório
- Consulte a documentação do Selenium

---

**Desenvolvido para automação e análise de dados do Uber Driver** 🚗💨
