/**
 * Main application logic.
 */

// Customer form handler
document.getElementById('customer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    clearResult('customer-result');

    const customerData = {
        name: document.getElementById('customer-name').value,
        email: document.getElementById('customer-email').value,
        company: document.getElementById('customer-company').value || null,
        phone: document.getElementById('customer-phone').value || null,
    };

    try {
        const customer = await customerAPI.create(customerData);
        showResult('customer-result', `Customer created successfully! ID: ${customer.id}`, 'success');
        document.getElementById('customer-form').reset();
    } catch (error) {
        showResult('customer-result', `Error: ${error.message}`, 'error');
    }
});

// Procurement form handler
document.getElementById('procurement-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    clearResult('procurement-result');

    const itemsText = document.getElementById('items').value;
    const items = itemsText.split('\n').map(item => item.trim()).filter(item => item);

    const requestData = {
        customer_id: parseInt(document.getElementById('customer-id').value),
        items: items,
        budget_limit: document.getElementById('budget-limit').value 
            ? parseFloat(document.getElementById('budget-limit').value) 
            : null,
    };

    try {
        const result = await procurementAPI.create(requestData);
        showResult('procurement-result', 
            `Procurement request created! Order ID: ${result.order_id}, Status: ${result.status}`, 
            'success');
        document.getElementById('procurement-form').reset();
        
        // Reload orders after a delay
        setTimeout(() => {
            loadOrders();
        }, 1000);
    } catch (error) {
        showResult('procurement-result', `Error: ${error.message}`, 'error');
    }
});

// Load orders handler
document.getElementById('load-orders').addEventListener('click', () => {
    loadOrders();
});

/**
 * Load and display orders.
 */
async function loadOrders() {
    const ordersList = document.getElementById('orders-list');
    showLoading('orders-list');

    const customerId = document.getElementById('filter-customer-id').value;
    const filterCustomerId = customerId ? parseInt(customerId) : null;

    try {
        const orders = await orderAPI.list(filterCustomerId);
        displayOrders(orders);
    } catch (error) {
        ordersList.innerHTML = `<div class="result error">Error loading orders: ${error.message}</div>`;
    }
}

/**
 * Display orders in the UI.
 */
function displayOrders(orders) {
    const ordersList = document.getElementById('orders-list');

    if (orders.length === 0) {
        ordersList.innerHTML = '<div class="result info">No orders found.</div>';
        return;
    }

    ordersList.innerHTML = orders.map(order => `
        <div class="order-card">
            <h3>Order #${order.id}</h3>
            <div class="order-info">
                <div><span>Customer ID:</span> ${order.customer_id}</div>
                <div><span>Status:</span> <span class="status ${order.status}">${order.status}</span></div>
                <div><span>Total Amount:</span> ${formatCurrency(order.total_amount)}</div>
                <div><span>Created:</span> ${formatDate(order.created_at)}</div>
            </div>
            ${order.items && order.items.length > 0 ? `
                <div style="margin-top: 10px;">
                    <strong>Items:</strong>
                    <ul style="margin-top: 5px; margin-left: 20px;">
                        ${order.items.map(item => `
                            <li>${item.item_name} (Qty: ${item.requested_quantity}) - ${item.status}</li>
                        `).join('')}
                    </ul>
                </div>
            ` : ''}
            ${order.notes ? `<div style="margin-top: 10px; color: #666;"><em>${order.notes}</em></div>` : ''}
        </div>
    `).join('');
}

// Load orders on page load
document.addEventListener('DOMContentLoaded', () => {
    loadOrders();
});

