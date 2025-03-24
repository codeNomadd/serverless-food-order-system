// API endpoint for our food delivery service
const API_BASE_URL = 'https://ptwq1ckzk7.execute-api.ap-northeast-2.amazonaws.com/prod';

// Get DOM elements we'll need
const loadingOverlay = document.getElementById('loadingOverlay');
const toast = document.getElementById('toast');
const createOrderForm = document.getElementById('createOrderForm');
const orderDetails = document.getElementById('orderDetails');
const orderIdDisplay = document.getElementById('orderIdDisplay');
const itemDisplay = document.getElementById('itemDisplay');

// Show/hide loading spinner during API calls
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Display toast messages for success/error feedback
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type === 'success' ? 'bg-green-500' : 'bg-red-500'}`;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// Validate order ID format (1-6 digits)
function validateOrderId(orderId) {
    return /^\d{1,6}$/.test(orderId);
}

// Validate item name (letters and spaces only, max 30 chars)
function validateItem(item) {
    return /^[A-Za-z\s]{1,30}$/.test(item);
}

// Display order details in the UI
function displayOrderDetails(order) {
    orderIdDisplay.textContent = order.orderId;
    itemDisplay.textContent = order.item;
    
    // Add a nice scale animation when showing details
    orderDetails.classList.add('animate-scale-in');
    setTimeout(() => {
        orderDetails.classList.remove('animate-scale-in');
    }, 300);
    
    orderDetails.classList.remove('hidden');
}

// Handle new order creation
createOrderForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const orderId = document.getElementById('newOrderId').value;
    const item = document.getElementById('newItem').value;

    // Validate inputs before sending
    if (!validateOrderId(orderId)) {
        showToast('Order ID must be 1-6 digits', 'error');
        return;
    }
    if (!validateItem(item)) {
        showToast('Item must be text only, max 30 characters', 'error');
        return;
    }

    // Show confirmation dialog
    const result = await Swal.fire({
        title: 'Confirm Order',
        text: `Create order #${orderId} for ${item}?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, create it!',
        cancelButtonText: 'Cancel'
    });

    if (result.isConfirmed) {
        try {
            showLoading();
            await axios.post(`${API_BASE_URL}/order`, { orderId, item });
            showToast('Order created successfully!');
            e.target.reset();
            displayOrderDetails({ orderId, item });
        } catch (error) {
            showToast(error.response?.data?.message || 'Error creating order', 'error');
        } finally {
            hideLoading();
        }
    }
});

// Handle order retrieval
async function getOrder() {
    const orderId = document.getElementById('searchOrderId').value;

    if (!validateOrderId(orderId)) {
        showToast('Please enter a valid Order ID (1-6 digits)', 'error');
        return;
    }

    try {
        showLoading();
        orderDetails.classList.add('hidden');
        const response = await axios.get(`${API_BASE_URL}/order?orderId=${orderId}`);
        displayOrderDetails(response.data);
        showToast('Order retrieved successfully!');
    } catch (error) {
        if (error.response?.status === 404) {
            orderIdDisplay.textContent = 'Not Found';
            itemDisplay.textContent = 'Order does not exist';
            orderDetails.classList.remove('hidden');
            showToast('Order not found', 'error');
        } else {
            showToast(error.response?.data?.message || 'Error fetching order', 'error');
        }
    } finally {
        hideLoading();
    }
}

// Show welcome message when page loads
Swal.fire({
    title: 'Welcome!',
    text: 'Ready to take your food order?',
    icon: 'info',
    timer: 2000,
    showConfirmButton: false,
    toast: true,
    position: 'top-end'
}); 