const express = require('express');
const path = require('path');
const router = express.Router();
const bodyParser = require('body-parser');
const app = express();

router.get('/',(req,res)=>{
    res.render('home/first');
});
router.post('/',(req,res)=>{
   if(req.body.choose === 'doctor'){
       res.redirect('/login');
   }
   else if(req.body.choose === 'patient'){
       res.redirect('/index');
   }

});
router.post('/index',(req,res)=>{
    console.log(req.body);
    res.redirect('/questions');

});
router.get('/index',(req,res)=>{
    res.render('home/index');
});
router.get('/questions',(req,res)=>{
    res.render('home/questions');
});
router.get('/login',(req,res)=>{
    res.render('home/login');
});
router.get('/chat',(req,res)=>{
    res.render('home/chat');
});
module.exports = router;