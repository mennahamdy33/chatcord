const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const router = express.Router();
const bodyParser = require('body-parser');
const app = express();

const doctors = [{
    id: "12345",
    password: "0000",
    name: "Fady"
},
{
    id: "54321",
    password: "1111",
    name: "Marwa"
},
{
    id: "98765",
    password: "2222",
    name: "Salma"
},
{
    id: "56789",
    password: "3333",
    name: "Menna"
},
{
    id: "14785",
    password: "4444",
    name: "Mohamed"
},
]
    


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
router.post('/login',(req,res)=>{
    var i=0;
    for (i =0 ; i<5; i++){
        if(doctors[i].id == req.body.id){
            var k = i;
        }   
    }
    if(req.body.id != doctors[k].id){
        res.redirect('/login');
    }
    else{
        if(req.body.password == doctors[k].password){
            res.redirect('/chat');
        }
        else{
            res.redirect('/login');
        }
    }
});
router.get('/chat',(req,res)=>{
    res.render('home/chat');
});
module.exports = router;