const ordersButton = document.querySelector('#orders');
tableContainer = document.querySelector('#table-container');
const ordersUrl = '/api/orders'

function clearHtml() {
  tableContainer.innerHTML = '';
}

function addRow_orders(item, tableBody, customersArr) {
  let customer = item["Customers"]
  let order = item["Orders"]
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  idCell.textContent = order.order_id;
  const customerIdCell = document.createElement('td');
  const orderDateCell = document.createElement('td');
  const totalAmountCell = document.createElement('td');

  const updateButtonCell = document.createElement('td');
  const updateButton = document.createElement('button');
  updateButton.textContent = 'Update';

  const deleteButtonCell = document.createElement('td');
  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';

  const customerIdSelect = document.createElement('select')
  const firstCustomerOp = document.createElement('option')
  firstCustomerOp.setAttribute('value', customer.customer_id);
  firstCustomerOp.setAttribute('selected', '');
  firstCustomerOp.setAttribute('hidden', '');
  firstCustomerOp.textContent = customer.first_name + ' ' + customer.last_name
  customerIdSelect.appendChild(firstCustomerOp);
  customersArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.customer_id)
    op.textContent = item.first_name + ' ' + item.last_name
    customerIdSelect.appendChild(op)
  });


  const orderDateInput = document.createElement('input')
  orderDateInput.setAttribute('type', 'date')
  orderDateInput.setAttribute('value', order.order_date);
  const totalAmountInput = document.createElement('input')
  totalAmountInput.setAttribute('type', 'number')
  totalAmountInput.setAttribute('step', 0.01)
  totalAmountInput.setAttribute('value', order.total_amount);

  customerIdCell.appendChild(customerIdSelect);
  orderDateCell.appendChild(orderDateInput);
  totalAmountCell.appendChild(totalAmountInput);

  updateButton.addEventListener('click', () => {
    const dataForAdd = {
      customer_id: customerIdSelect.value, 
      order_date: orderDateInput.value, 
      total_amount: totalAmountInput.value,
    };

    fetch(ordersUrl + '/' + idCell.textContent, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.ok) {
        console.log('Данные успешно обновлены');
      } else {
        console.error('Произошла ошибка при обновлении данных');
      }
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_orders(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  deleteButton.addEventListener('click', () => {
    fetch(ordersUrl + '/' + idCell.textContent, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.ok) {
        console.log('Данные успешно обновлены');
      } else {
        console.error('Произошла ошибка при обновлении данных');
      }
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_orders(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  updateButtonCell.appendChild(updateButton);
  deleteButtonCell.appendChild(deleteButton);

  row.appendChild(idCell);
  row.appendChild(customerIdCell);
  row.appendChild(orderDateCell);
  row.appendChild(totalAmountCell);
  row.appendChild(updateButtonCell);
  row.appendChild(deleteButton);
  tableBody.appendChild(row);
}

function addButton_orders(tableBody, customersArr) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  const customerIdCell = document.createElement('td');
  const orderDateCell = document.createElement('td');
  const totalAmountCell = document.createElement('td');

  const addButtonCell = document.createElement('td');
  const addButton = document.createElement('button');
  addButton.textContent = 'Add';

  const customerIdSelect = document.createElement('select')
  const firstCustomerOp = document.createElement('option')
  firstCustomerOp.setAttribute('selected', '');
  firstCustomerOp.setAttribute('hidden', '');
  firstCustomerOp.textContent = 'Choose a customer'
  customerIdSelect.appendChild(firstCustomerOp);
  customersArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.customer_id)
    op.textContent = item.first_name + ' ' + item.last_name
    customerIdSelect.appendChild(op)
  });


  const orderDateInput = document.createElement('input')
  orderDateInput.setAttribute('type', 'date')
  const totalAmountInput = document.createElement('input')
  totalAmountInput.setAttribute('type', 'number')
  totalAmountInput.setAttribute('step', 0.01)
  totalAmountInput.setAttribute('value', 0);

  customerIdCell.appendChild(customerIdSelect);
  orderDateCell.appendChild(orderDateInput);
  totalAmountCell.appendChild(totalAmountInput);

  addButton.addEventListener('click', () => {
    const dataForAdd = {
      customer_id: customerIdSelect.value, 
      order_date: orderDateInput.value, 
      total_amount: totalAmountInput.value,
    };
    console.log(dataForAdd)
    fetch(ordersUrl, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.ok) {
        console.log('Данные успешно обновлены');
      } else {
        console.error('Произошла ошибка при обновлении данных');
      }
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_orders(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  });

  addButtonCell.appendChild(addButton);

  row.appendChild(idCell);
  row.appendChild(customerIdCell);
  row.appendChild(orderDateCell);
  row.appendChild(totalAmountCell);
  row.appendChild(addButtonCell);
  tableBody.appendChild(row);
}

function fillTableContainer_orders(data) {
  clearHtml()
  tableContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th></th>
          <th>Customer</th>
          <th>Order date</th>
          <th>Total amount</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
      `
  let arr = data["orders"];
  let customersArr = data["customers"];
  const tableBody = tableContainer.querySelector('tbody');

  arr.forEach(item => addRow_orders(item, tableBody, customersArr));
  addButton_orders(tableBody, customersArr)
}

ordersButton.addEventListener('click', () => {
  fetch(ordersUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fillTableContainer_orders(data);
})});