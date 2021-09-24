import React, { FC } from 'react'
import './Home.css'
import { ReactComponent as Logo } from './ParrotPen.svg'


function Home<FC>() {
    return (

        <div>

            <div className="container">
                <h1 className="hero-header"> كلام  </h1>
                <h2 className="hero-subheading">Stay Connected, The Halal Way.</h2>
                {/* <h2 className="hero-subheading"></h2> */}

            </div>
            <LoginSection />
        </div>
    )
}

function LoginSection<FC>() {
    return (
        <div className="login-container">
            <Logo className="logo" />
            <form action="">
                <input type="text" name="username" placeholder="Username or Email" id="" className="input-field" />
                <input type="text" name="password" placeholder="Password" id="" className="input-field" />
                <input type="submit" value="Log In" className="input-field primary-button" />
            </form>
            <a href="http://example.com">Forgot Password?</a>
            <hr style={{ width: '90%', height: 0 }} />
            <button className="input-field"></button>
        </div>
    )
}
export default Home
