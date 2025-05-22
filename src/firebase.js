// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCkTPaKPCOPMrSZBjXLoatwhsLYQEXH_sw",
  authDomain: "bookie-ai-dc1f8.firebaseapp.com",
  projectId: "bookie-ai-dc1f8",
  storageBucket: "bookie-ai-dc1f8.firebasestorage.app",
  messagingSenderId: "1075298251385",
  appId: "1:1075298251385:web:e5fd21c540f0f961589aa8",
  measurementId: "G-NQKNNMEG28"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);
const auth = getAuth(app);

export { db, auth };