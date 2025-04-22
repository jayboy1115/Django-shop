// src/components/checkout/PaymentSection.jsx
import { useState } from 'react';
import styles from './PaymentSection.module.css';
import { BsFillCreditCard2FrontFill } from 'react-icons/bs';
import { FaCcPaypal } from 'react-icons/fa';
import api from '../../api';

const PaymentSection = () => {
    const cart_code = localStorage.getItem('cart_code');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const makePayment = async () => {
        if (!cart_code) {
            setError('Cart code is missing');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const res = await api.post('/initiate_payment/', { cart_code });
            console.log('Flutterwave response:', res.data);
            window.location.href = res.data.data.link;
        } catch (err) {
            console.error('Flutterwave error:', err);
            setError(err.response?.data?.detail || 'Failed to initiate Flutterwave payment');
        } finally {
            setLoading(false);
        }
    };

    const paypalPayment = async () => {
        if (!cart_code) {
            setError('Cart code is missing');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const res = await api.post('/initiate_paypal_payment/', { cart_code });
            console.log('PayPal response:', res.data);
            if (res.data.approval_url) {
                window.location.href = res.data.approval_url;
            } else {
                setError('No PayPal approval URL provided');
            }
        } catch (err) {
            console.error('PayPal error:', err);
            setError(err.response?.data?.error || 'Failed to initiate PayPal payment');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="col-md-4">
            <div className={`card ${styles.card}`}>
                <div className="card-header" style={{ backgroundColor: '#6050DC', color: 'white' }}>
                    <h5>Payment Options</h5>
                </div>
                <div className="card-body">
                    {/* PayPal Button */}
                    <button
                        className={`btn btn-primary w-100 mb-3 ${styles.paypalButton}`}
                        onClick={paypalPayment}
                        id="paypal-button"
                        disabled={loading}
                    >
                        <FaCcPaypal style={{ fontSize: '30px' }} /> Pay with PayPal
                    </button>

                    {/* Flutterwave Button */}
                    <button
                        className={`btn btn-warning w-100 ${styles.flutterwaveButton}`}
                        onClick={makePayment}
                        id="flutterwave-button"
                        disabled={loading}
                    >
                        <BsFillCreditCard2FrontFill style={{ fontSize: '30px' }} /> Pay with Flutterwave
                    </button>

                    {/* Error Message */}
                    {error && <p className="text-danger mt-3">{error}</p>}
                </div>
            </div>
        </div>
    );
};

export default PaymentSection;