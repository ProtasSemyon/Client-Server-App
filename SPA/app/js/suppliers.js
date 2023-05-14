const suppliersButton = document.querySelector('#suppliers');
tableContainer = document.querySelector('#table-container');
const suppliersUrl = '/api/suppliers'

function clearHtml() {
  tableContainer.innerHTML = '';
}

function addRow_suppliers(item, tableBody) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  idCell.textContent = item.supplier_id;
  const supplierNameCell = document.createElement('td');
  const contactNameCell = document.createElement('td');
  const emailCell = document.createElement('td');
  const phoneCell = document.createElement('td');

  const updateButtonCell = document.createElement('td');
  const updateButton = document.createElement('button');
  updateButton.textContent = 'Update';

  const deleteButtonCell = document.createElement('td');
  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';

  const supplierNameInput = document.createElement('input')
  supplierNameInput.setAttribute('type', 'text')
  supplierNameInput.setAttribute('value', item.supplier_name);
  const contactNameInput = document.createElement('input')
  contactNameInput.setAttribute('type', 'text')
  contactNameInput.setAttribute('value', item.contact_name);
  const emailInput = document.createElement('input')
  emailInput.setAttribute('type', 'text')
  emailInput.setAttribute('value', item.email);
  const phoneInput = document.createElement('input')
  phoneInput.setAttribute('type', 'text')
  phoneInput.setAttribute('value', item.phone);

  supplierNameCell.appendChild(supplierNameInput);
  contactNameCell.appendChild(contactNameInput);
  emailCell.appendChild(emailInput);
  phoneCell.appendChild(phoneInput);

  updateButton.addEventListener('click', () => {
    const dataForAdd = {
      supplier_name: supplierNameInput.value, 
      contact_name: contactNameInput.value, 
      email: emailInput.value,
      phone: phoneInput.value
    };

    const jwt_token = localStorage.getItem('jwt_token');

    fetch(suppliersUrl + '/' + idCell.textContent, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json',
        'Authorization' :'Bearer '+ jwt_token
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
      fillTableContainer_suppliers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  deleteButton.addEventListener('click', () => {
    const jwt_token = localStorage.getItem('jwt_token');

    fetch(suppliersUrl + '/' + idCell.textContent, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' :'Bearer '+ jwt_token
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
      fillTableContainer_suppliers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  updateButtonCell.appendChild(updateButton);
  deleteButtonCell.appendChild(deleteButton);

  row.appendChild(idCell);
  row.appendChild(supplierNameCell);
  row.appendChild(contactNameCell);
  row.appendChild(emailCell);
  row.appendChild(phoneCell);
  row.appendChild(updateButtonCell);
  row.appendChild(deleteButton);
  tableBody.appendChild(row);
}

function addButton_suppliers(tableBody) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  const supplierNameCell = document.createElement('td');
  const contactNameCell = document.createElement('td');
  const emailCell = document.createElement('td');
  const phoneCell = document.createElement('td');

  const addButtonCell = document.createElement('td');
  const addButton = document.createElement('button');
  addButton.textContent = 'Add';

  const supplierNameInput = document.createElement('input')
  supplierNameInput.setAttribute('type', 'text')

  const contactNameInput = document.createElement('input')
  contactNameInput.setAttribute('type', 'text')

  const emailInput = document.createElement('input')
  emailInput.setAttribute('type', 'text')

  const phoneInput = document.createElement('input')
  phoneInput.setAttribute('type', 'text')


  supplierNameCell.appendChild(supplierNameInput);
  contactNameCell.appendChild(contactNameInput);
  emailCell.appendChild(emailInput);
  phoneCell.appendChild(phoneInput);


  addButton.addEventListener('click', () => {
    const dataForAdd = {
      supplier_name: supplierNameInput.value, 
      contact_name: contactNameInput.value, 
      email: emailInput.value,
      phone: phoneInput.value
    };

    const jwt_token = localStorage.getItem('jwt_token');

    fetch(suppliersUrl, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json',
        'Authorization' :'Bearer '+ jwt_token
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
      fillTableContainer_suppliers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  });

  addButtonCell.appendChild(addButton);

  row.appendChild(idCell);
  row.appendChild(supplierNameCell);
  row.appendChild(contactNameCell);
  row.appendChild(emailCell);
  row.appendChild(phoneCell);
  row.appendChild(addButtonCell);
  tableBody.appendChild(row);
}

function fillTableContainer_suppliers(data) {
  clearHtml()
  tableContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th></th>
          <th>Supplier name</th>
          <th>Contact name</th>
          <th>E-mail</th>
          <th>Phone</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
      `
  let arr = data["suppliers"];
  const tableBody = tableContainer.querySelector('tbody');

  arr.forEach(item => addRow_suppliers(item, tableBody));
  addButton_suppliers(tableBody)
}

suppliersButton.addEventListener('click', () => {
  fetch(suppliersUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fillTableContainer_suppliers(data);
})});