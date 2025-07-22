import OrderHistoryItem from "./OrderHistoryItem"

const OrderHistoryItemContainer = ({orderitems}) => {
  return (
    <div className="row" style={{height: "300px", overflow:"auto"}}>
    <div className="col-md-12">
      <div className="card">
        <div className="card-header" style={{ backgroundColor: '#6050DC', color: 'white' }}>
          <h5>Order History</h5>
        </div>

        {orderitems.length > 0 ? (
          orderitems.map(item => <OrderHistoryItem key={item.id} item={item} />)
        ) : (
          <div className="card-body text-center">
            <p>No order history available</p>
          </div>
        )}
      </div>
    </div>
  </div>
  )
}

export default OrderHistoryItemContainer;
