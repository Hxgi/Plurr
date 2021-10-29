import React, { useState, useEffect, Fragment } from 'react';


function Dashboard (props){
  const [userEmail, setUserEmail] = useState('');
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState([]);

  
  useEffect(() => {
    if (localStorage.getItem('token') === null) {
      window.location.replace('http://localhost:3000/login');
    } else {
      fetch('http://127.0.0.1:8000/service/authors/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then(response => response.json())
        .then((response) => {
          console.log(response)
            setItems({items: response.items});
            setLoading(false);

        })
    }
  },[]
  
  );
  

  return (
    <div>
      {loading === false && (
        <Fragment>

                    {items.items.map(name => (  
          <ul>  
                <li><a href={name.id}>{name.displayName} </a></li>
                <li><a href={name.github}>GitHub</a></li>
                <img class="fit-picture"
                    src={name.profileImage} 
                    alt={name.displayName}>
                </img>
            </ul>  
        ))}
        </Fragment>
      )}
    </div>
  );
};

export default Dashboard;

