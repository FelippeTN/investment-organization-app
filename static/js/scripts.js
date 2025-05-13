document.addEventListener('DOMContentLoaded', function () {
    const portfolioCanvas = document.getElementById('portfolioChart');
    if (portfolioCanvas) {
        try {
            const loadingSpinner = portfolioCanvas.parentElement.querySelector('.chart-loading');
            if (loadingSpinner) loadingSpinner.classList.remove('hidden'); // Show spinner
            portfolioCanvas.classList.add('opacity-50'); // Add loading state
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
                                '#1E3A8A', // Deep Navy
                                '#3B82F6', // Bright Blue
                                '#10B981', // Emerald Green
                                '#F59E0B', // Amber
                                '#EF4444', // Red
                                '#8B5CF6', // Purple
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
                portfolioCanvas.classList.remove('opacity-50'); // Remove loading state
                if (loadingSpinner) loadingSpinner.classList.add('hidden'); // Hide spinner
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
            if (loadingSpinner) loadingSpinner.classList.remove('hidden'); // Show spinner
            sectorCanvas.classList.add('opacity-50'); // Add loading state
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
                sectorCanvas.classList.remove('opacity-50'); // Remove loading state
                if (loadingSpinner) loadingSpinner.classList.add('hidden'); // Hide spinner
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
    const welcomeChatInput = document.getElementById('chat-input'); // Initial input in welcome-container
    const welcomeSendButton = document.getElementById('send-button'); // Initial button in welcome-container
    const chatContainer = document.getElementById('chat-container');
    const welcomeContainer = document.getElementById('welcome-container');
    const inputContainer = document.getElementById('input-container');
    let isFirstMessage = true;

    // After first message, switch to the input-container's input and button
    const chatInput = inputContainer.querySelector('#chat-input');
    const sendButton = inputContainer.querySelector('#send-button');

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `p-3 rounded-lg max-w-[80%] ${
            isUser ? 'bg-blue-100 text-blue-900 ml-auto' : 'bg-gray-100 text-gray-900 mr-auto'
        }`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage(inputElement) {
        const message = inputElement.value.trim();
        if (!message) return;

        // On first message, transition to chat view
        if (isFirstMessage) {
            welcomeContainer.classList.add('hidden');
            chatContainer.classList.remove('hidden');
            inputContainer.classList.remove('hidden');
            isFirstMessage = false;

            // Disable welcome input and button to prevent further use
            welcomeChatInput.disabled = true;
            welcomeSendButton.disabled = true;
        }

        // Add user message
        addMessage(message, true);
        inputElement.value = '';

        // Disable input and button while waiting for response
        const currentInput = isFirstMessage ? welcomeChatInput : chatInput;
        const currentButton = isFirstMessage ? welcomeSendButton : sendButton;
        currentInput.disabled = true;
        currentButton.disabled = true;

        try {
            const response = await fetch('http://26.159.78.241:8080/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama',
                    messages: [
                        { role: 'user', content: message }
                    ],
                    max_tokens: 500,
                    temperature: 0.7
                })
            });

            if (!response.ok) throw new Error('Erro na resposta do servidor');

            const data = await response.json();
            const aiMessage = data.choices[0].message.content;
            addMessage(aiMessage, false);
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            addMessage('Desculpe, ocorreu um erro ao processar sua mensagem.', false);
        } finally {
            currentInput.disabled = false;
            currentButton.disabled = false;
            currentInput.focus();
        }
    }

    // Event listeners for welcome input and button
    welcomeSendButton.addEventListener('click', () => sendMessage(welcomeChatInput));
    welcomeChatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage(welcomeChatInput);
    });

    // Event listeners for chat input and button (used after first message)
    sendButton.addEventListener('click', () => sendMessage(chatInput));
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage(chatInput);
    });
});