from voice_ai_agent.main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from Voice AI Agent!" in captured.out
