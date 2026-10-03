import pytest
from tax_split import calculate_refund_split

def test_hybrid_progressive_with_exact_taxes():
    """Tests refund split using exact payslip tax withholdings (synthetic dataset)."""
    result = calculate_refund_split(
        a=72500, b=48000,
        c=2150, d=3400,
        tax1=22055.80, return_amount=3120.40,
        actual_tax_man=15240.50, actual_tax_woman=6815.30
    )

    # Monetary amounts
    assert result['man_amount'] == pytest.approx(1982.33, abs=0.01)
    assert result['woman_amount'] == pytest.approx(1138.07, abs=0.01)

    # Percentage breakdown
    assert result['man_percent'] == pytest.approx(63.53, abs=0.01)
    assert result['woman_percent'] == pytest.approx(36.47, abs=0.01)

def test_linear_fallback_no_exact_taxes():
    """Tests the fallback calculation when exact tax deductions are omitted."""
    result = calculate_refund_split(
        a=72500, b=48000,
        c=2150, d=3400,
        tax1=22055.80, return_amount=3120.40
    )

    assert result['man_amount'] == pytest.approx(1681.52, abs=0.01)
    assert result['woman_amount'] == pytest.approx(1438.88, abs=0.01)
    assert result['man_percent'] == pytest.approx(53.89, abs=0.01)
    assert result['woman_percent'] == pytest.approx(46.11, abs=0.01)

def test_zero_total_income():
    """Tests that the script safely exits if total income is zero."""
    with pytest.raises(SystemExit) as exc_info:
        calculate_refund_split(a=0, b=0, c=0, d=0, tax1=0, return_amount=0)
    assert exc_info.value.code == 1

def test_costs_exceed_income():
    """Tests that the script exits if costs exceed gross income."""
    with pytest.raises(SystemExit) as exc_info:
        calculate_refund_split(
            a=10000, b=10000,
            c=15000, d=15000,
            tax1=5000, return_amount=1000,
            actual_tax_man=2500, actual_tax_woman=2500
        )
    assert exc_info.value.code == 1
