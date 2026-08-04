// frontend/firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    getAuth, 
    GoogleAuthProvider, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    signInWithPopup, 
    updateProfile,
    onAuthStateChanged,
    signOut 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// Web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAuz5yAIO3BTxkMa5IyLDgqaxdhH-KRLPg",
  authDomain: "study-sprint-ai.firebaseapp.com",
  projectId: "study-sprint-ai",
  storageBucket: "study-sprint-ai.firebasestorage.app",
  messagingSenderId: "349772054285",
  appId: "1:349772054285:web:de8302751db39534beba44",
  measurementId: "G-HZX7V3ZF1Z"
};

// Initialize Firebase & Auth Services
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

// Export modules for signup.html, login.html, and studio.html
export { 
    auth, 
    googleProvider, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    signInWithPopup, 
    updateProfile,
    onAuthStateChanged,
    signOut 
};