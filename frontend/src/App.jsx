import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ForgotPassword from './pages/forgotPassword'
import Layout from './components/shared/layout';
import Dashboard from './components/dashboard';
import Login from './pages/login';
import Studies from './pages/studies';
import Patients from './pages/patients';
import History from './pages/history';
import Messages from './pages/messages';
import Register from './pages/register';
import ResetPassword from './pages/resetPassword'
import Shared from './pages/shared';
import PrivateRoute from './components/PrivateRoute';
import { Fragment } from 'react';

function App() {
  return (
    <Router>
      <Fragment>
        <Routes>
          <Route path="/" element={<Layout />} >
            <Route exact path='/' element={<PrivateRoute />}>
              <Route index element={<Dashboard />} />
            </Route>
            <Route exact path='/studies' element={<PrivateRoute />}>
              <Route index element={<Studies />} />
            </Route>
            <Route exact path='/history' element={<PrivateRoute />}>
              <Route index element={<History />} />
            </Route>
            <Route exact path='/shared' element={<PrivateRoute />}>
              <Route index element={<Shared />} />
            </Route>
            <Route exact path='/patients' element={<PrivateRoute />}>
              <Route index element={<Patients />} />
            </Route>
            <Route exact path='/messages' element={<PrivateRoute />}>
              <Route index element={<Messages />} />
            </Route>
          </Route>
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register/>} />
          <Route path="forgot-password" element={<ForgotPassword />} />
          <Route path="reset-password" element={<ResetPassword />} />
        </Routes>
      </Fragment>
    </Router>
  );
}

export default App;
