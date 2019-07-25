@extends('layouts.app')

@inject('Message', 'App\Http\Controllers\MessageController')
@inject('User', 'App\User')
@php
    $msgs = $Message->get_all();
@endphp
@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">Dashboard</div>

                <div class="card-body">
                    @if (session('status'))
                        <div class="alert alert-success" role="alert">
                            {{ session('status') }}
                        </div>
                    @endif

                    <hr>
                    <h2>Mensagens Enviadas</h2>
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col">Por</th>
                                <th scope="col">Destinatario</th>
                                <th scope="col">Conteudo<th>
                                <th scope="col">Estado<th>
                            </tr>
                        </thead>
                        @foreach($msgs as $msg)    
                            <tbody>
                                <tr>
                                    <td> {{ $User::find($msg->user_id)->name }} </td>
                                    <td> {{ $msg->recipient }} </td>
                                    <td> {{ $msg->content }} </td>
                                    <td> {{ $msg->status }} </td>
                                </tr>
                            </tbody>
                        @endforeach
                    </table>
                    <hr>
                    <h2>Nova Mensagem</h2>
                    <form method="POST" action="{{ route('msg.insert') }}">
                        @csrf
                        <div class="form-group">
                            <label for="exampleInputEmail1">Destinatario</label>
                            <input type="text" class="form-control" name="recipient" placeholder="Destinatario">
                        </div>
                        <div class="form-group">
                            <label for="exampleInputEmail1">Mensagem</label>
                            <input type="text" class="form-control" name="content" placeholder="Mensagem">
                        </div>
                        <button type="submit" class="btn btn-primary">Adicionar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
