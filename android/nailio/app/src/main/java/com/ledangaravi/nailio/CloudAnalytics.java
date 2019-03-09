package com.ledangaravi.nailio;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

class CloudApi {

    RequestQueue queue;
    String url;

    CloudApi(Context context)
    {
        queue = Volley.newRequestQueue(context);
        url = "https://35.204.14.232:6065";
    }


    public void requestAnalytics(String imageBase64, String UID, Response.Listener<JSONObject> responseListener) throws JSONException {


        JSONObject jsonBody = new JSONObject();
        jsonBody.put("Image",imageBase64);
        jsonBody.put("UID",UID);

        // Request a string response from the provided URL.
        JsonObjectRequest jsonRequest = new JsonObjectRequest(Request.Method.POST, url, jsonBody,
                responseListener, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("Network error","An error occured while sending image")
            }
        });

        queue.add(jsonRequest);

    }
}
