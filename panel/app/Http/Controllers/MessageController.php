<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\User;
use App\Message;
use Auth;
use Hash;

class MessageController extends Controller {


    public function insert(Request $request) {
        $msg = new Message();
        $msg->user_id       = Auth::User()->id;
        $msg->recipient     = $request->recipient;
        $msg->content       = $request->content;
        $msg->status        = 0;
        $msg->save();
        return redirect()->route('home.message');
    }


    public function get_all() {
        return Message::where('user_id', Auth::User()->id)->get();
    }

    public function delete($id) {
        $user = User::find($id); 
        if( $user->leader_id == Auth::User()->id ) {
            $user->delete();
        }
        return redirect()->route('home.message');
    }
}
