import { useEffect, useState } from 'react';
import UserInfo from './UserInfo';
import OrderHistoryItemContainer from './OrderHistoryItemContainer';
import Spinner from '../ui/Spinner';
import api from '../../api';

const UserProfilePage = () => {
    const [userInfo, setUserInfo] = useState({});
    const [orderitems, setOrderitems] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        setError(null);
        api.get('/user_info/')
            .then(res => {
                console.log(res.data);
                setUserInfo({ username: res.data.username, email: res.data.email });
                setOrderitems(res.data.items || []);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching user info:', err.message);
                setError('Failed to load user profile');
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <Spinner loading={loading} />;
    }

    if (error) {
        return <p className="text-danger">{error}</p>;
    }

    return (
        <div className="container my-5">
            <UserInfo userInfo={userInfo} />
            <OrderHistoryItemContainer orderitems={orderitems} />
        </div>
    );
};

export default UserProfilePage;