/**
 * API client for communicating with the backend.
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Make an API request.
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * Customer API methods.
 */
const customerAPI = {
    create: (customerData) => apiRequest('/customers/', {
        method: 'POST',
        body: customerData,
    }),
    list: () => apiRequest('/customers/'),
    get: (customerId) => apiRequest(`/customers/${customerId}`),
    update: (customerId, customerData) => apiRequest(`/customers/${customerId}`, {
        method: 'PUT',
        body: customerData,
    }),
    delete: (customerId) => apiRequest(`/customers/${customerId}`, {
        method: 'DELETE',
    }),
};

/**
 * Procurement API methods.
 */
const procurementAPI = {
    create: (requestData) => apiRequest('/procurement/', {
        method: 'POST',
        body: requestData,
    }),
};

/**
 * Order API methods.
 */
const orderAPI = {
    list: (customerId = null) => {
        const params = customerId ? `?customer_id=${customerId}` : '';
        return apiRequest(`/orders/${params}`);
    },
    get: (orderId) => apiRequest(`/orders/${orderId}`),
    updateStatus: (orderId, status) => apiRequest(`/orders/${orderId}/status`, {
        method: 'PATCH',
        body: { status },
    }),
};

/**
 * Health check.
 */
const healthAPI = {
    check: () => apiRequest('/health/'),
};

