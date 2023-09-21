import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/shared/layout';
import Dashboard from './components/dashboard';
import Products from './components/products';
import Login from './components/login';
import BookSearch from './components/BookSearch'

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={ <Layout /> }>
          <Route index element={ <Dashboard/> }/>
          <Route path='products' element={ <Products/> }/>
        </Route>
        <Route path='login' element={ <Login/> }/>
        <Route path='bookSearch' element = { <BookSearch/> }/>
    </Routes>
    </Router>
  );
}

export default App;
