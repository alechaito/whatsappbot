<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');

#Team Routes
Route::post('/agent/insert', 'UserController@insert_agent')->name('agent.insert');
Route::get('/user/delete/{id}', 'UserController@delete')->name('user.delete');

#WhatsApp Connect
Route::get('/qrcode', 'HomeController@qr_code')->name('qrcode');
