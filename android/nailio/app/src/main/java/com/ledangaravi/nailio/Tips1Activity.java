package com.ledangaravi.nailio;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class Tips1Activity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tips1);

        TextView textView = findViewById(R.id.tips1_custom);

        Intent intent = getIntent();
        String verdict = intent.getStringExtra(EvalActivity.EVAL_MESSAGE);

        if(verdict.equals("normal")){
            textView.setText(getResources().getString(R.string.nailed_it));
        }
    }
}
