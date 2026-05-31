import express from 'express';
import bodyParser from 'body-parser';
import { createReadStream } from 'fs';
import crypto from 'crypto';
import http from 'http';
import CORS from 'cors';
import puppeteer from 'puppeteer';
import createApp from './app.js';

const app = createApp(express, bodyParser, createReadStream, crypto, http, CORS, puppeteer);

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
