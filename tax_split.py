import argparse
import sys

def calculate_refund_split(a, b, c, d, tax1, return_amount, actual_tax_man=None, actual_tax_woman=None):
    total_income = a + b
    if total_income == 0:
        print("Error: Total income cannot be zero.")
        sys.exit(1)

    # Step 1: Establish initial tax paid (Scaled perfectly to match TAX1)
    if actual_tax_man is not None and actual_tax_woman is not None:
        total_exact = actual_tax_man + actual_tax_woman
        # Scale exact inputs up/down slightly so they equal exactly TAX1 (handles Kirchensteuer/Soli discrepancies)
        paid_man = tax1 * (actual_tax_man / total_exact)
        paid_woman = tax1 * (actual_tax_woman / total_exact)
    else:
        # Fallback to linear distribution if exact payslips aren't provided
        paid_man = tax1 * (a / total_income)
        paid_woman = tax1 * (b / total_income)

    # Step 2: Calculate individual effective tax rates on Gross Income
    rate_man = paid_man / a
    rate_woman = paid_woman / b

    # Step 3: Calculate "Virtual Tax Liability" by applying rates to Net Income (Income - Costs)
    net_man = max(0, a - c)
    net_woman = max(0, b - d)

    virtual_tax_man = net_man * rate_man
    virtual_tax_woman = net_woman * rate_woman
    total_virtual_tax = virtual_tax_man + virtual_tax_woman

    if total_virtual_tax <= 0:
        print("Error: Total virtual tax base is zero. Costs exceed incomes.")
        sys.exit(1)

    # Step 4: Split the actual final tax bill based on the Virtual Tax ratio
    final_tax_owed = tax1 - return_amount
    fair_tax_man = final_tax_owed * (virtual_tax_man / total_virtual_tax)
    fair_tax_woman = final_tax_owed * (virtual_tax_woman / total_virtual_tax)

    # Step 5: Final Refund is what you initially paid minus what you fairly owe
    refund_man = paid_man - fair_tax_man
    refund_woman = paid_woman - fair_tax_woman

    return {
        'man_amount': refund_man,
        'man_percent': (refund_man / return_amount) * 100,
        'woman_amount': refund_woman,
        'woman_percent': (refund_woman / return_amount) * 100
    }

def main():
    parser = argparse.ArgumentParser(description="Calculate fair split of a joint tax refund factoring in both progressive rates and individual work costs.")

    parser.add_argument('-a', '--income-man', type=float, required=True, help="Man's Income (A)")
    parser.add_argument('-b', '--income-woman', type=float, required=True, help="Woman's Income (B)")
    parser.add_argument('-c', '--costs-man', type=float, required=True, help="Man's working costs (C)")
    parser.add_argument('-d', '--costs-woman', type=float, required=True, help="Woman's working costs (D)")
    parser.add_argument('-t', '--tax1', type=float, required=True, help="Total initial tax paid (TAX1)")
    parser.add_argument('-r', '--return-amount', type=float, required=True, help="Total tax returned (RETURN)")

    parser.add_argument('--exact-tax-man', type=float, help="Exact initial tax paid by the man (optional)")
    parser.add_argument('--exact-tax-woman', type=float, help="Exact initial tax paid by the woman (optional)")

    args = parser.parse_args()

    result = calculate_refund_split(
        args.income_man, args.income_woman,
        args.costs_man, args.costs_woman,
        args.tax1, args.return_amount,
        args.exact_tax_man, args.exact_tax_woman
    )

    print("-" * 50)
    print("Tax Refund Split Calculator (Progressive + Costs Adjusted)")
    print("-" * 50)
    print(f"Total Refund:   €{args.return_amount:,.2f}\n")
    print(f"Man's Share:    €{result['man_amount']:,.2f} ({result['man_percent']:.1f}%)")
    print(f"Woman's Share:  €{result['woman_amount']:,.2f} ({result['woman_percent']:.1f}%)")
    print("-" * 50)

if __name__ == "__main__":
    main()
