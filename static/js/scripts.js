document.addEventListener('DOMContentLoaded', function () {
    const portfolioCanvas = document.getElementById('portfolioChart');
    if (portfolioCanvas) {
        try {
            const loadingSpinner = portfolioCanvas.parentElement.querySelector('.chart-loading');
            if (loadingSpinner) loadingSpinner.classList.remove('hidden');
            portfolioCanvas.classList.add('opacity-50');
            const operations = JSON.parse(portfolioCanvas.dataset.operations || '[]');

            const portfolio = {};
            operations.forEach(op => {
                const ticker = op.ticker;
                const quantity = parseFloat(op.quantity);
                const unitaryPrice = parseFloat(op.unitary_price.toString().replace(',', '.'));
                const type = op.type.toLowerCase();

                if (!portfolio[ticker]) {
                    portfolio[ticker] = { quantity: 0, totalValue: 0, totalCost: 0 };
                }

                if (type === 'compra') {
                    portfolio[ticker].quantity += quantity;
                    portfolio[ticker].totalCost += quantity * unitaryPrice;
                } else if (type === 'venda') {
                    portfolio[ticker].quantity -= quantity;
                    portfolio[ticker].totalCost -= quantity * unitaryPrice;
                }

                if (portfolio[ticker].quantity > 0) {
                    portfolio[ticker].totalValue = portfolio[ticker].quantity * (portfolio[ticker].totalCost / portfolio[ticker].quantity);
                } else {
                    portfolio[ticker].totalValue = 0;
                }
            });

            const labels = [];
            const values = [];
            for (const ticker in portfolio) {
                if (portfolio[ticker].quantity > 0 && portfolio[ticker].totalValue > 0) {
                    labels.push(ticker);
                    values.push(portfolio[ticker].totalValue);
                }
            }

            if (labels.length > 0 && values.length > 0) {
                const ctx = portfolioCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: [
                                '#1E3A8A',
                                '#3B82F6',
                                '#10B981',
                                '#F59E0B',
                                '#EF4444',
                                '#8B5CF6',
                            ],
                            borderColor: '#FFFFFF',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#1F2937',
                                    font: {
                                        size: 14,
                                        weight: '500'
                                    }
                                }
                            },
                            tooltip: {
                                backgroundColor: '#111827',
                                titleColor: '#FFFFFF',
                                bodyColor: '#D1D5DB',
                                callbacks: {
                                    label: function (context) {
                                        let label = context.label || '';
                                        let value = context.raw || 0;
                                        return `${label}: R$ ${value.toFixed(2)}`;
                                    }
                                }
                            }
                        }
                    }
                });
                portfolioCanvas.classList.remove('opacity-50');
                if (loadingSpinner) loadingSpinner.classList.add('hidden');
            }
        } catch (error) {
            console.error('Erro ao renderizar o gráfico de portfólio:', error);
            portfolioCanvas.classList.remove('opacity-50');
            if (loadingSpinner) loadingSpinner.classList.add('hidden');
        }
    }

    const sectorCanvas = document.getElementById('sectorChart');
    if (sectorCanvas) {
        try {
            const loadingSpinner = sectorCanvas.parentElement.querySelector('.chart-loading');
            if (loadingSpinner) loadingSpinner.classList.remove('hidden');
            sectorCanvas.classList.add('opacity-50');
            const sectors = JSON.parse(sectorCanvas.dataset.sectors || '{}');

            const labels = [];
            const values = [];
            for (const sector in sectors) {
                if (sectors[sector] > 0) {
                    labels.push(sector);
                    values.push(sectors[sector]);
                }
            }

            if (labels.length > 0 && values.length > 0) {
                const ctx = sectorCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: [
                                '#1E3A8A',
                                '#3B82F6',
                                '#10B981',
                                '#F59E0B',
                                '#EF4444',
                                '#8B5CF6',
                            ],
                            borderColor: '#FFFFFF',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#1F2937',
                                    font: {
                                        size: 14,
                                        weight: '500'
                                    }
                                }
                            },
                            tooltip: {
                                backgroundColor: '#111827',
                                titleColor: '#FFFFFF',
                                bodyColor: '#D1D5DB',
                                callbacks: {
                                    label: function (context) {
                                        let label = context.label || '';
                                        let value = context.raw || 0;
                                        return `${label}: R$ ${value.toFixed(2)}`;
                                    }
                                }
                            }
                        }
                    }
                });
                sectorCanvas.classList.remove('opacity-50');
                if (loadingSpinner) loadingSpinner.classList.add('hidden');
            }
        } catch (error) {
            console.error('Erro ao renderizar o gráfico de setores:', error);
            sectorCanvas.classList.remove('opacity-50');
            if (loadingSpinner) loadingSpinner.classList.add('hidden');
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `user-message ${isUser ? 'user-message' : 'ai-message'} animate-fade-in`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        chatInput.value = '';
        chatInput.disabled = true;
        sendButton.disabled = true;

        try {
            const response = await fetch('http://26.159.78.241:8080/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama',
                    messages: [
                        { role: 'system', content: 'Você é um analista profissional do mercado financeiro e que tira duvida dos usuarios com base nas informações de suas carteiras de investimentos.' },
                        { role: 'user', content: message }
                    ],
                    max_tokens: 500,
                    temperature: 0.7,
                    stream: true
                })
            });

            if (!response.ok) throw new Error('Erro na resposta do servidor');

            const aiMessageDiv = document.createElement('div');
            aiMessageDiv.className = 'ai-message animate-fade-in';
            chatMessages.appendChild(aiMessageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let aiMessage = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim().startsWith('data: '));

                for (const line of lines) {
                    const jsonData = line.replace('data: ', '').trim();
                    if (jsonData === '[DONE]') continue;

                    try {
                        const parsed = JSON.parse(jsonData);
                        const content = parsed.choices[0].delta.content;
                        if (content) {
                            aiMessage += content;
                            aiMessageDiv.textContent = aiMessage;
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                            await new Promise(resolve => setTimeout(resolve, 10));
                        }
                    } catch (e) {
                        console.warn('Erro ao parsear chunk:', e);
                    }
                }
            }

            if (!aiMessage) {
                aiMessageDiv.textContent = 'Nenhuma resposta recebida.';
            }
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            addMessage('Desculpe, ocorreu um erro ao processar sua mensagem.', false);
        } finally {
            chatInput.disabled = false;
            sendButton.disabled = false;
            chatInput.focus();
        }
    }

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    addMessage('Bem-vindo ao AI Chat! Como posso ajudar você hoje?', false);
});