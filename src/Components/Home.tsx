import React, { FC } from 'react'
import './Home.css'
import { ReactComponent as Logo } from './ParrotPen.svg'
import Button from '@mui/material/Button'
import { styled } from '@mui/material/styles'
import Paper from '@mui/material/Paper'

function Home<FC>() {
    return (

        <div className="container">
            <h1 className="hero-header"> كلام  </h1>
            <h2 className="hero-subheading">Stay Connected, The Halal Way.</h2>


            <LoginSection />
        </div>
    )
}

const InputButton = styled(Button)({
    marginTop: '30px',
    height: '60px',
    fontSize: '36px',
    marginBottom: '20px',
    textTransform: 'capitalize'
})
function LoginSection<FC>() {
    return (
        <Paper elevation={6} className="login-container">
            <Logo className="logo" />

            <input type="text" name="username" placeholder="Username or Email" id="" className="input-field" />
            <input type="password" name="password" placeholder="Password" id="" className="input-field" />
            <InputButton className="input-field" color="primary" variant="contained">Log in</InputButton>

            <a href="http://example.com" style={{ marginBottom: '10px', fontSize: '18px' }}>Forgot Password?</a>
            <hr style={{ width: '90%', height: 0 }} />
            <InputButton className="input-field" variant="contained" color="secondary">Sign Up</InputButton>
        </Paper>
    )
}
export default Home
