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

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={ <Layout /> }>
          <Route index element={ <Dashboard/> }/>
          <Route path='studies' element={ <Studies />}/>
          <Route path='history' element={ <History />} />
          <Route path='shared' element={ <Shared />} />
          <Route path='patients' element={ <Patients /> } />
          <Route path='messages' element={ <Messages /> } />
        </Route>
        <Route path='login' element={ <Login/> }/>
        <Route path='register' element={ <Register/> } />
        <Route path='forgot-password' element={ <ForgotPassword />} />
        <Route path='reset-password' element={ <ResetPassword />} />
      </Routes>
    </Router>
  );
}

export default App;
