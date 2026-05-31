import express from 'express';
import bodyParser from 'body-parser';
import { createReadStream } from 'fs';
import crypto from 'crypto';
import http from 'http';
import path from 'path';
import mongoose from 'mongoose';
import cors from 'cors'
import axios from 'axios'
import morgan from 'morgan'
import pug from 'pug'
import puppeteer from 'puppeteer';
import createProxyMiddleware from 'http-proxy-middleware';


import initializeApp from './app.js'

const app = initializeApp(express, bodyParser, createReadStream, crypto, http, path, mongoose, cors, axios, morgan, pug, puppeteer, createProxyMiddleware)
const PORT = 3000

app.listen(PORT, () => {
  console.log('Сервер запущен на порту 3000');
});
